import os

# ==========================================
# SHUTDOWN PC
# ==========================================

def shutdown_pc():

    os.system("shutdown /s /t 1")

# ==========================================
# RESTART PC
# ==========================================

def restart_pc():

    os.system("shutdown /r /t 1")

# ==========================================
# LOCK PC
# ==========================================

def lock_pc():

    os.system("rundll32.exe user32.dll,LockWorkStation")

# ==========================================
# OPEN TASK MANAGER
# ==========================================

def open_task_manager():

    os.system("start taskmgr")