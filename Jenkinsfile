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
            sh 'docker build -f sp_mon/Dockerfile -t registry.sonata-nfv.eu:5000/son-monitor-spprobe:v4.0 .'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker build -f vm_mon/Dockerfile -t registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v4.0 .'
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
        stage('son-monitor-spprobe') {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-spprobe:v4.0'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v4.0'
          }
        }
      }
    }
    stage('Deployment in sta-sp-v4.0') {
      parallel {
        stage('Deployment in sta-sp-v4.0') {
          steps {
            echo 'Deploying in sta-sp-v4.0...'
          }
        }
        stage('Deploying') {
          steps {
            sh 'rm -rf tng-devops || true'
            sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
            dir(path: 'tng-devops') {
              sh 'ansible-playbook roles/sp.yml -i environments -e "target=sta-sp-v4.0 component=monitoring"'
            }
          }
        }
      }
    }
    stage('Promoting containers to integration env') {
      parallel {
        stage('Publishing containers to int') {
          steps {
            echo 'Promoting containers to integration'
          }
        }
        stage('son-monitor-spprobe') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-spprobe:v4.0 registry.sonata-nfv.eu:5000/son-monitor-spprobe:v4.0'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-spprobe:v4.0'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v4.0 registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v4.0'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v4.0'
          }
        }
      }
    }
    stage('Deployment in integration') {
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
              sh 'ansible-playbook roles/sp.yml -i environments -e "target=int-sp component=monitoring"'
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