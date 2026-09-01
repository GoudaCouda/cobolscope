# Build script for ProLeap CLI Java components
# Compiles all Java sources with Java 17 release compatibility into lib/

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$libDir = Join-Path $scriptDir "lib"
$pkgLibDir = Join-Path (Join-Path $scriptDir "cobolscope") "lib"
$javaJar = Join-Path $pkgLibDir "proleap-cobol-parser.jar"

if (!(Test-Path $javaJar)) {
    $javaJar = Join-Path $libDir "proleap-cobol-parser.jar"
}

if (!(Test-Path $javaJar)) {
    Write-Error "Could not find proleap-cobol-parser.jar"
    exit 1
}

if (!(Test-Path $libDir)) {
    New-Item -ItemType Directory -Path $libDir -Force | Out-Null
}

$javaFiles = Get-ChildItem -Path "$scriptDir\java" -Filter "*.java" -Recurse | Select-Object -ExpandProperty FullName

Write-Host "Compiling $($javaFiles.Count) Java source files with --release 17..." -ForegroundColor Cyan

& javac --release 17 -cp $javaJar -d $libDir $javaFiles

if ($LASTEXITCODE -eq 0) {
    Write-Host "Java compilation successful! Bundling classes into JAR..." -ForegroundColor Green
    python -c "import zipfile, glob, os; jar_path = '$($javaJar.Replace('\', '/'))'; zf = zipfile.ZipFile(jar_path, 'a'); [zf.write(f, os.path.basename(f)) for f in glob.glob('$($libDir.Replace('\', '/'))/*.class')]; zf.close()"
    Write-Host "Updated JAR with bundled classes at $javaJar" -ForegroundColor Green
} else {
    Write-Error "Java compilation failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
