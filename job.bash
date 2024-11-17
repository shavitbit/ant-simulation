ids=("27.0-1.5-1.0-5.0" "21.0-1.6-1.1-5.1" "22.0-1.7-1.2-5.2")

for id in "${ids[@]}"; do
  # Create the Job
  job_name="antscli-job-${id//./-}"
  cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: $job_name
spec:
  template:
    spec:
      containers:
      - name: cli-container
        image: philipsinfo/antcli:0.0.1
        args: ["run", "--rounds", "10", "--id", "${id}", "-c", "http://flask-web-svc:5000/api/v1/send_sim_result"]
      restartPolicy: Never
EOF

  echo "Created Job $job_name"

  # Wait for the Job to complete
  while true; do
    job_status=$(kubectl get job $job_name -o jsonpath='{.status.succeeded}')
    if [[ "$job_status" == "1" ]]; then
      echo "Job $job_name completed successfully."
      break
    fi
    echo "Waiting for Job $job_name to finish..."
    sleep 30
  done
  echo "Logs for job $job_name:"
  kubectl logs job/$job_name
  kubectl delete job $job_name
done