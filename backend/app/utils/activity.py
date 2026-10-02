"""Helper pencatatan aktivitas admin."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.admin_log import AdminActivityLog


def log_admin_activity(
    db: Session,
    admin_id: Optional[int],
    action: str,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    description: Optional[str] = None,
) -> None:
    """
    Menyimpan satu baris ke admin_activity_logs.
    Contoh action: approve_doctor, reject_doctor, suspend_user,
                   create_slider, update_report_status, login, logout.
    """
    log = AdminActivityLog(
        admin_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        description=description,
    )
    db.add(log)
