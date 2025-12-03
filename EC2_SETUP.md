# EC2 Setup for YOLO Training

## Option 1: GPU Instance (Recommended)

**Instance Type**: `g4dn.xlarge` (4 vCPU, 16GB RAM, 1x T4 GPU)
**AMI**: `ami-08b736afa17db122b` (Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.8)
**Storage**: 50GB gp3
**Training Time**: 30-45 minutes
**Cost**: ~$0.50

## Option 2: CPU Instance (Slower)

**Instance Type**: `t2.xlarge` (4 vCPU, 16GB RAM, NO GPU)
**AMI**: `ami-08b736afa17db122b` (same AMI works)
**Storage**: 30GB gp3
**Training Time**: 6-8 hours
**Cost**: ~$1.50

## 2. Quick Launch Commands

```bash
# Connect to instance (Amazon Linux 2023)
ssh -i your-key.pem ec2-user@your-ec2-ip

# Verify GPU
nvidia-smi

# Upload files
scp -i your-key.pem arc_training_data.zip ec2-user@your-ec2-ip:~/
scp -i your-key.pem YOLO_Training_Final.ipynb ec2-user@your-ec2-ip:~/

# Start Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser
```

## 3. Training

1. Open browser: `http://your-ec2-ip:8888`
2. Open `YOLO_Training_Final.ipynb`
3. Run all cells (auto-detects GPU/CPU)
4. Download `wall_model_gpu.pt` or `wall_model_cpu.pt`

## 4. Recommendation

**For Hackathon**: Use `g4dn.xlarge` - 10x faster training!
**If Budget Tight**: Use `t2.xlarge` but start training immediately (8 hours)