# EC2 Detailed Setup Guide

## Step 1: Launch Instance

### Option A: GPU Instance (Preferred)
1. **Go to AWS Console** → EC2 → Launch Instance
2. **Name**: `arc-yolo-training`
3. **AMI**: Search `ami-08b736afa17db122b` → Select
4. **Instance Type**: `g4dn.xlarge`

### Option B: CPU Instance (If GPU quota unavailable)
1. **Instance Type**: `c5.2xlarge` (8 vCPU, 16GB)
2. **Training Time**: 2-3 hours (vs 45 minutes GPU)
3. **Cost**: ~$0.60 total
5. **Key Pair**: Create new or select existing `.pem` file
6. **Security Group**: Create new with:
   - SSH (22) - Your IP
   - Custom TCP (8888) - Your IP
7. **Storage**: 50GB gp3
8. **Click Launch Instance**

## Step 2: Connect to Instance

```bash
# Wait 2-3 minutes for instance to start
# Get Public IP from EC2 console

# Connect (replace with your key and IP)
ssh -i your-key.pem ec2-user@your-public-ip

# Verify GPU
nvidia-smi
# Should show: Tesla T4 GPU
```

## Step 3: Upload Files

```bash
# From your local machine (new terminal)
scp -i your-key.pem arc_training_data.zip ec2-user@your-public-ip:~/
scp -i your-key.pem YOLO_Training_Final.ipynb ec2-user@your-public-ip:~/
```

## Step 4: Start Jupyter

```bash
# Back in SSH session
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# Copy the token from output (looks like: ?token=abc123...)
```

## Step 5: Access Jupyter

1. **Browser**: `http://your-public-ip:8888`
2. **Paste token** from Step 4
3. **Open**: `YOLO_Training_Final.ipynb`

## Step 6: Run Training

1. **Cell 1**: Install dependencies (30 seconds)
2. **Cell 2**: Extract dataset (2 minutes)
3. **Cell 3**: Check GPU detected
4. **Cell 4**: Train model (30-45 minutes)
5. **Cell 5**: Validate results
6. **Cell 6**: Save model

## Step 7: Download Model

1. **Jupyter**: Right-click `wall_model_gpu.pt` → Download
2. **Copy to**: Your Arc project folder
3. **Update**: `dual_detection_service.py` to use new model

## Step 8: Cleanup

```bash
# Stop instance to avoid charges
# EC2 Console → Select instance → Instance State → Stop
```

## Troubleshooting

**Can't connect**: Check security group allows your IP on port 22
**No GPU**: Verify `g4dn.xlarge` instance type selected
**Jupyter won't start**: Try `pip install jupyter` first
**Upload fails**: Check file paths and key permissions (`chmod 400 your-key.pem`)

## Expected Results

- **Training Time**: 30-45 minutes (GPU) or 2-3 hours (CPU)
- **Cost**: ~$0.40 (GPU) or ~$0.60 (CPU)
- **Model Accuracy**: 85%+ mAP50
- **Output**: `wall_model_gpu.pt` ready for Arc project