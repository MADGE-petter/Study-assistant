
!define APPNAME "Study Assistant"
!define VERSION "1.0.0"
!define PUBLISHER "Study Assistant Team"

Name "${APPNAME}"
OutFile "${APPNAME} Setup.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File /r "dist\StudyAssistant\*"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\StudyAssistant.exe"
    CreateShortCut "$STARTMENU\Programs\${APPNAME}.lnk" "$INSTDIR\StudyAssistant.exe"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\${APPNAME}.lnk"
    Delete "$STARTMENU\Programs\${APPNAME}.lnk"
    RMDir /r "$INSTDIR"
SectionEnd
