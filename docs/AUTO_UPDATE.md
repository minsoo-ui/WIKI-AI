# Auto Update GitHub (Manual Run)

## Muc tieu
- Backup toan bo thay doi len GitHub de recover khi can.
- Chay bang tay tren may local, khong phu thuoc browser.

## File script
- `scripts/auto_update_github.ps1`
- `scripts/run_auto_update.bat`
- Log: `logs/auto-update.log`

## Cach chay nhanh
- Double click `scripts/run_auto_update.bat`
- Hoac CMD/PowerShell:
  - `scripts\run_auto_update.bat`
  - `scripts\run_auto_update.bat "backup: before major refactor"`

## Cach chay truc tiep PowerShell
- `powershell -ExecutionPolicy Bypass -File scripts\auto_update_github.ps1`
- `powershell -ExecutionPolicy Bypass -File scripts\auto_update_github.ps1 -Message "backup: update docs"`

## Hanh vi script
1. `git add -A`
2. Neu co thay doi: `git commit`
3. `git pull --rebase origin main`
4. `git push origin main`
5. Ghi log ket qua vao `logs/auto-update.log`

## Luu y
- Can dang nhap GitHub credential/token tren may.
- Neu muon bo qua pull/rebase:
  - `powershell -ExecutionPolicy Bypass -File scripts\auto_update_github.ps1 -SkipPull`
