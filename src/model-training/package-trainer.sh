# creates a trainer.tar.gz file with all training code inside
# script uploads packaged file to gcs bucket --> instacap-trainer.tar.gz
rm -f trainer.tar trainer.tar.gz
tar cvf trainer.tar package
gzip trainer.tar
gsutil cp trainer.tar.gz $GCS_BUCKET_URI/instacap-trainer.tar.gz