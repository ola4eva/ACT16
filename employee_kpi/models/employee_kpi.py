# -*- coding: utf-8 -*-

from urllib.parse import urlencode, urljoin
from odoo import models, fields, api

SELECTION_KPI = [
    ("draft", "New"),
    ("sent", "Sent To Employee"),
    ("manager", "Manager To Assess"),
    ("done", "Manager Assessed"),
]


class EmployeeKpi(models.Model):
    _name = "employee_kpi.employee_kpi"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "Employee Performance Assessment"

    def _get_default_user_id(self):
        return self.env.uid

    name = fields.Char(
        string="NAME",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="ASSIGNEE",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    department_id = fields.Many2one(
        "hr.department",
        string="UNIT",
        required=True,
        related="employee_id.department_id",
    )
    job_id = fields.Many2one(
        "hr.job",
        string="POSITION",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    period = fields.Char(
        string="PERIOD",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    parent_id = fields.Many2one(
        "hr.employee",
        string="Assessor",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    user_id = fields.Many2one(
        "res.users", string="Responsible", default=_get_default_user_id
    )
    state = fields.Selection(
        SELECTION_KPI,
        string="State",
        default="draft",
        tracking=True,
    )
    question_ids = fields.One2many(
        "employee_kpi.question", "kpi_id", string="Questions"
    )
    template_id = fields.Many2one(
        comodel_name="employee_kpi.kpi.template",
        string="Template",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    hr_comment = fields.Text("HR's comments")
    md1_comment = fields.Text("First MD's comments")
    md2_comment = fields.Text("First MD's comments")
    url = fields.Char("url", compute="_get_record_url")

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        value = {"value": {}}
        if self.employee_id:
            department_id = (
                self.employee_id.department_id and self.employee_id.department_id.id
            )
            job_id = self.employee_id.job_id and self.employee_id.job_id.id
            parent_id = self.employee_id.parent_id and self.employee_id.parent_id.id
            value["value"].update(
                {
                    "department_id": department_id,
                    "job_id": job_id,
                    "parent_id": parent_id,
                }
            )
        return value

    @api.onchange("template_id")
    def _onchange_template_id(self):
        if self.template_id:
            self.question_ids.unlink()
            Question = self.env["employee_kpi.question"].sudo()
            for question in self.template_id.question_ids:
                kpi_question = Question.create(
                    {
                        "name": question.name,
                        "weight": question.weight,
                        "target": question.target,
                        "state": self.state,
                    }
                )
                self.question_ids += kpi_question

    def action_send_to_employee(self):
        # send an email to employee
        template = self.env.ref(
            "employee_kpi.employee_kpi_request_email_to_employee")
        template.send_mail(self.id, force_send=True)
        self.state = "sent"

    def action_send_to_manager(self):
        # send an email to manager
        template = self.env.ref(
            "employee_kpi.employee_kpi_request_email_to_employee_manager"
        )
        template.send_mail(self.id, force_send=True)
        self.state = "manager"

    def action_complete_assessment(self):
        # send notification to hr manager
        template = self.env.ref(
            "employee_kpi.employee_kpi_completion_email_to_hr")
        template.send_mail(self.id, force_send=True)
        self.state = "done"

    def _get_record_url(self):
        base_url = self.get_base_url()
        params = {
            "id": self.id,
            "cids": self.id,
            "action": int(self.env.ref("employee_kpi.employee_kpi_action")),
            "model": self._name,
            "menu_id": int(self.env.ref("employee_kpi.employee_kpi_root_menu")),
            "view_type": "form",
        }
        url = f"{base_url}/web#{urlencode(params)}"
        self.url = url


class EmployeeKpiQuestion(models.Model):
    _name = "employee_kpi.question"
    _description = "Employee KPI Question"

    name = fields.Char(string="Key Performance Indicators",
                       readonly=True, states={'draft': [('readonly', False)]})
    weight = fields.Float("Weight", readonly=True, states={
                          'draft': [('readonly', False)]})
    target = fields.Float("Target", readonly=True, states={
                          'draft': [('readonly', False)]})
    self_rating = fields.Float("Self Rating", readonly=True, states={
                               'sent': [('readonly', False)]})
    manager_rating = fields.Float("Manager's Rating", readonly=True, states={
                                  'manager': [('readonly', False)]})
    manager_comment = fields.Char("Manager's Comment", readonly=True, states={
                                  'manager': [('readonly', False)]})
    kpi_id = fields.Many2one("employee_kpi.employee_kpi", string="KPI")
    is_section = fields.Boolean("Is Section")
    state = fields.Selection(related="kpi_id.state")

    @api.constrains("target")
    def _constrains_target(self):
        for record in self:
            if record.target > 100:
                raise ValueError("Target cannot exceed 100%")

    @api.constrains("self_rating")
    def _constrains_self_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Self rating cannot exceed 100%")

    @api.constrains("manager_rating")
    def _constrains_manager_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Manager rating cannot exceed 100%")
