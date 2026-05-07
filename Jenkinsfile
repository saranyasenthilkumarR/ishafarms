pipeline {
  agent any

  environment {
    AWS_REGION      = 'ap-south-1'
    AWS_ACCOUNT_ID  = '885160773251'
    ECR_REGISTRY    = "${88516077325}.dkr.ecr.${ap-south-1}.amazonaws.com"
    S3_FRONTEND     = 'isha-farms-frontend'
    S3_ARTIFACTS    = 'isha-farms-artifacts'
  }

 stages {

    stage('Checkout') {
      steps {
        echo 'Cloning Isha Farms repo...'
        checkout scm
      }
    }

    stage('Build Docker Images') {
      parallel {
        stage('Product Service') {
          steps {
            sh 'docker build -t product-service:latest ./product-service'
          }
        }
        stage('User Service') {
          steps {
            sh 'docker build -t user-service:latest ./user-service'
          }
        }
        stage('Order Service') {
          steps {
            sh 'docker build -t order-service:latest ./order-service'
          }
        }
      }
    }

    stage('Push to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION | \
          docker login --username AWS --password-stdin $ECR_REGISTRY

          docker tag product-service:latest $ECR_REGISTRY/product-service:latest
          docker push $ECR_REGISTRY/product-service:latest

          docker tag user-service:latest $ECR_REGISTRY/user-service:latest
          docker push $ECR_REGISTRY/user-service:latest

          docker tag order-service:latest $ECR_REGISTRY/order-service:latest
          docker push $ECR_REGISTRY/order-service:latest
        '''
      }
    }

    stage('Upload Frontend to S3') {
      steps {
        sh 'aws s3 sync ./frontend s3://$S3_FRONTEND --delete'
      }
    }

    stage('Health Check') {
      steps {
        echo 'Build and push complete!'
        sh 'docker images | grep -E "product|user|order"'
      }
    }

  }

  post {
    success {
      echo '✅ Isha Farms pipeline SUCCESS!'
    }
    failure {
      echo '❌ Pipeline FAILED - check logs above!'
    }
  }
}
