from odoo import SUPERUSER_ID


from .constants import IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS


def get_attachments_with_google_fonts(env):
    domain = [
        ("public", "=", True),
        ("url", "!=", False),
        ("name", "in", IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS),
        ("res_model", "=", "ir.ui.view"),
        ("res_id", "=", 0),
        ("create_uid", "=", SUPERUSER_ID),
    ]

    attachments = env["ir.attachment"].sudo().search(domain)
    return attachments


def delete_attachments_with_google_fonts(env):
    attachments = get_attachments_with_google_fonts(env)
    attachments.unlink()

    num_attachments = len(attachments)

    return num_attachments