from odoo import models, api, fields


class CompetenceValidation(models.Model):
    _name = 'training.competence.validation'
    _description = "Competence validation"

    @api.model
    def validate_competences(self):
        # Get all partners
        partners = self.env['res.partner'].search([])

        # Remove all category_ids from partners
        partners.write({'category_id': [(5,)]})
        partners.write({'locomotive': [(5,)]})

        # Iterate over each partner
        for partner in partners:
            # Get valid exams linked to the partner
            valid_exams = self.env['training.exam'].search([
                ('person', '=', partner.id),
                ('valid_until', '>=', fields.Date.today())
            ])

            # Get the category ids of valid exams
            valid_category_ids = valid_exams.mapped('competence').ids

            # Set the category_ids from valid exams
            partner.write({'category_id': [(6, 0, valid_category_ids)]})

            valid_locomotive_ids = valid_exams.mapped('vte_locomotive').ids
            partner.write({'locomotive': [(6, 0, valid_locomotive_ids)]})

        # Commit the changes to the database
        self.env.cr.commit()

