{{- define "runner-fleet.name" -}}
runner-fleet-platform
{{- end }}

{{- define "runner-fleet.labels" -}}
app.kubernetes.io/name: {{ include "runner-fleet.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
