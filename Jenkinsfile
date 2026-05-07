pipeline {
  agent any

  environment {
    AWS_REGION      = 'ap-south-1'
    AWS_ACCOUNT_ID  = '885160773251'
    ECR_REGISTRY    = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    S3_FRONTEND     = 'isha-farms-frontend'
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
          aws ecr get-login-password --region ap-south-1 | \
          docker login --username AWS --password-stdin 885160773251.dkr.ecr.ap-south-1.amazonaws.com

          docker tag product-service:latest 885160773251.dkr.ecr.ap-south-1.amazonaws.com/product-service:latest
          docker push 885160773251.dkr.ecr.ap-south-1.amazonaws.com/product-service:latest

          docker tag user-service:latest 885160773251.dkr.ecr.ap-south-1.amazonaws.com/user-service:latest
          docker push 885160773251.dkr.ecr.ap-south-1.amazonaws.com/user-service:latest

          docker tag order-service:latest 885160773251.dkr.ecr.ap-south-1.amazonaws.com/order-service:latest
          docker push 885160773251.dkr.ecr.ap-south-1.amazonaws.com/order-service:latest
        '''
      }
    }

    stage('Upload Frontend to S3') {
      steps {
        sh 'aws s3 sync ./frontend s3://isha-farms-frontend --delete'
      }
    }

    stage('Health Check') {
      steps {
        echo 'Build and push complete!'
        sh 'docker images | grep -E "product-service|user-service|order-service"'
      }
    }

  }

  post {
    success {
      echo '✅ Isha Farms deployed successfully!'
    }
    failure {
      echo '❌ Pipeline FAILED - check logs!'
    }
  }
}
