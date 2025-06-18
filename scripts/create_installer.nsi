Outfile "{{OUTPUT_FILE}}"
InstallDir $PROGRAMFILES\{{APP_NAME}}
Page directory
Page instfiles

Section "Install"
  SetOutPath $INSTDIR
  File /r "dist\\{{APP_NAME}}-win_x64\\*.*"
  CreateShortcut "$DESKTOP\\{{APP_NAME}}.lnk" "$INSTDIR\\{{APP_NAME}}.exe"
SectionEnd
