pipeline {
  agent any
  stages {
    stage('Container Build') {
      parallel {
        stage('Container Build') {
          steps {
            echo 'Building..'
          }
        }
        stage('son-monitor-spprobe') {
          steps {
            sh 'docker build -t registry.sonata-nfv.eu:5000/son-monitor-spprobe -f sp_mon/Dockerfile sp_mon/'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker build -t registry.sonata-nfv.eu:5000/son-monitor-vmprobe -f sp_mon/Dockerfile vm_mon/'
          }
        }
      }
    }
    stage('Unit Tests') {
      steps {
        echo 'Unit Testing..'
      }
    }
    stage('Code Style check') {
      steps {
        echo 'Code Style check....'
      }
    }
    stage('Containers Publication') {
      parallel {
        stage('Containers Publication') {
          steps {
            echo 'Publication of containers in local registry....'
          }
        }
        stage('son-monitor-spprobe) {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-spprobe'
          }
        }
        stage('son-monitor-vmprobe) {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-vmprobe'
          }
        }
      }
    }
    stage('Deployment in Integration') {
      parallel {
        stage('Deployment in Integration') {
          steps {
            echo 'Deploying in integration...'
          }
        }
        stage('Deploying') {
          steps {
            sh 'rm -rf tng-devops || true'
            sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
            dir(path: 'tng-devops') {
              sh 'ansible-playbook roles/sp.yml -i environments -e "target=pre-int-sp"'
            }
          }
        }
      }
    }
    stage('Promoting containers to integration env') {
      when {
         branch 'master'
      }
      parallel {
        stage('Publishing containers to int') {
          steps {
            echo 'Promoting containers to integration'
          }
        }
        stage('son-monitor-spprobe') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-spprobe:latest registry.sonata-nfv.eu:5000/son-monitor-spprobe:int'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-spprobe:int'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-vmprobe:latest registry.sonata-nfv.eu:5000/son-monitor-vmprobe:int'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-vmprobe:int'
          }
        }
      }
    }
    stage('Deployment in integration') {
      when {
         branch 'master'
      }
      parallel {
        stage('Deployment in integration') {
          steps {
            echo 'Deploying in integration...'
          }
        }
        stage('Deploying') {
          steps {
            sh 'rm -rf tng-devops || true'
            sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
            dir(path: 'tng-devops') {
              sh 'ansible-playbook roles/sp.yml -i environments -e "target=int-sp"'
            }
          }
        }
      }
    }
  }
  post {
    success {
      emailext(subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'", body: """<p>SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""", recipientProviders: [[$class: 'DevelopersRecipientProvider']])
      
    }
    failure {
      emailext(subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'", body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""", recipientProviders: [[$class: 'DevelopersRecipientProvider']])
      
    }
    
  }
}