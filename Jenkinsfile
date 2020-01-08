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
            sh 'docker build -f sp_mon/Dockerfile -t registry.sonata-nfv.eu:5000/son-monitor-spprobe .'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker build -f vm_mon/Dockerfile -t registry.sonata-nfv.eu:5000/son-monitor-vmprobe .'
          }
        }
        stage('tng-monitor-stats_collector') {
          steps {
            sh 'docker build -f cnf_mon/Dockerfile -t registry.sonata-nfv.eu:5000/tng-stats-collector .'
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
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-spprobe'
          }
        }
        stage('son-monitor-vmprobe') {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-vmprobe'
          }
        }
        stage('tng-monitor-stats_collector') {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/tng-stats-collector'
          }
        }
      }
    }
    stage('Deployment in pre-int') {
      parallel {
        stage('Deployment in pre-int') {
          steps {
            echo 'Deploying in pre-int...'
          }
        }
        stage('Deploying') {
          steps {
            sh 'rm -rf tng-devops || true'
            sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
            dir(path: 'tng-devops') {
              sh 'ansible-playbook roles/sp.yml -i environments -e "target=pre-int-sp component=monitoring"'
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
        stage('tng-monitor-stats_collector') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/tng-stats-collector:latest registry.sonata-nfv.eu:5000/tng-stats-collector:int'
            sh 'docker push  registry.sonata-nfv.eu:5000/tng-stats-collector:int'
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
    stage('Promoting release v5.1') {
        when {
            branch 'v5.1'
        }
        stages {
            stage('Generating release') {
                steps {
                    sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-spprobe:latest registry.sonata-nfv.eu:5000/son-monitor-spprobe:v5.1'
                    sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-vmprobe:latest registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v5.1'
                    sh 'docker tag registry.sonata-nfv.eu:5000/tng-stats-collector:latest registry.sonata-nfv.eu:5000/tng-stats-collector:v5.1'

                    sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-spprobe:v5.1'
                    sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-vmprobe:v5.1'
                    sh 'docker push  registry.sonata-nfv.eu:5000/tng-stats-collector:v5.1'
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
