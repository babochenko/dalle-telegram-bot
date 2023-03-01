gcloud functions deploy dalle-tg-bot \
  --runtime=python311 \
  --region=europe-west3 \
  --source=./dalletgbot/ \
  --entry-point=generate_images \
  --env-vars-file .env.yaml \
  --trigger-http \
  --allow-unauthenticated
