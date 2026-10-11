from typing import List, Tuple

MODULE = {
    "code": "leave_elm",
    "label": "Leave Management",
    "icon": "FaCalendarCheck",
    "base_path": "/leave",
    "nav_section": "Leave",
    "sort_order": 20,
    "status": "active"
}

NAV_ITEMS: List[dict] = [
    {
        "code": "leave.applications",
        "label": "My Leave",
        "icon": "FaCalendarAlt",
        "to": "/leave/applications",
        "required_permission": "leave_elm.application.view",
        "sort_order": 10
    },
    {
        "code": "leave.approvals",
        "label": "Approvals",
        "icon": "FaCheckCircle",
        "to": "/leave/approvals",
        "required_permission": "leave_elm.application.approve",
        "sort_order": 20
    }
]

PERMISSIONS: List[Tuple[str, str]] = [
    ("leave_elm.application.view", "See leave applications"),
    ("leave_elm.application.apply", "Submit a leave application"),
    ("leave_elm.application.approve", "Approve or reject a leave application")
]

ROLE_GRANTS = {
    "Employee": ["leave_elm.application.view", "leave_elm.application.apply"],
    "faculty": ["leave_elm.application.view", "leave_elm.application.apply"],
    "staff": ["leave_elm.application.view", "leave_elm.application.apply"],
    "Leave Approver": ["leave_elm.application.view", "leave_elm.application.approve"],
    "HOD": ["leave_elm.application.view", "leave_elm.application.approve"]
}
