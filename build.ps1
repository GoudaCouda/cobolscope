$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python (Join-Path $scriptDir "build_java.py")
exit $LASTEXITCODE
