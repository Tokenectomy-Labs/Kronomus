# ⚡ Kronumos Kairos — Windows Automated Cryptographic Installer
# Powered by Tokenectomy Labs (https://github.com/Tokenectomy-Labs/Kronomus)

$ErrorActionPreference = "Stop"

$Repo = "Tokenectomy-Labs/Kronomus"
$Tag = "v1.1.0"
$DebUrl = "https://github.com/$Repo/releases/download/$Tag/kronumos_1.1.0_amd64.deb"
$TarUrl = "https://github.com/$Repo/releases/download/$Tag/kronumos-linux-amd64.tar.gz"

Write-Host ""
Write-Host "    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ███████╗" -ForegroundColor Cyan
Write-Host "    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔═══██╗██╔════╝" -ForegroundColor Cyan
Write-Host "    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗" -ForegroundColor Cyan
Write-Host "    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║" -ForegroundColor Cyan
Write-Host "    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║" -ForegroundColor Cyan
Write-Host "    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "                     · K R O N U M O S   K A I R O S ·" -ForegroundColor Yellow
Write-Host "               Autonomous Code Remediation & SRE Agent • Windows" -ForegroundColor DarkGray
Write-Host ""

# Check for WSL (Windows Subsystem for Linux)
$hasWsl = Get-Command "wsl" -ErrorAction SilentlyContinue

Write-Host "⚡ Checking Windows environment..." -ForegroundColor White

if ($hasWsl) {
    Write-Host "✓ Detected WSL (Windows Subsystem for Linux)." -ForegroundColor Green
    Write-Host "  Installing Kronumos inside your WSL Linux environment for native compiler access..." -ForegroundColor Gray
    
    try {
        wsl bash -c "curl -fsSL https://raw.githubusercontent.com/$Repo/main/cli/install.sh | bash"
        Write-Host ""
        Write-Host "✅ Kronumos successfully installed into WSL!" -ForegroundColor Green
        Write-Host "  To run from PowerShell or CMD, simply type:" -ForegroundColor White
        Write-Host "    wsl kronumos" -ForegroundColor Cyan
        Write-Host "    wsl kronumos --fix" -ForegroundColor Cyan
        Write-Host ""
        exit 0
    } catch {
        Write-Warning "WSL installation encountered a warning. Proceeding with Windows direct setup."
    }
} else {
    Write-Host "ℹ WSL not detected on this system." -ForegroundColor Yellow
    Write-Host "  Recommendation: Run 'wsl --install' in an Administrator PowerShell to enable WSL 2" -ForegroundColor Gray
    Write-Host "  for native access to Linux test runners (pytest, cargo, npm, docker)." -ForegroundColor Gray
}

# Standalone setup path
$InstallDir = "$env:LOCALAPPDATA\Programs\Kronumos"
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

Write-Host "📦 Preparing Kronumos environment in: $InstallDir" -ForegroundColor White
Write-Host "  For full autonomous TDD loop on Windows, please run Kronumos within WSL or Docker." -ForegroundColor Gray
Write-Host ""
Write-Host "Visit https://github.com/$Repo for Windows documentation and updates." -ForegroundColor Cyan
Write-Host ""
