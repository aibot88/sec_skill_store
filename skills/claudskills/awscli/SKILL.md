---
name: awscli
description: "Referência e guia de uso do AWS CLI para gerenciar recursos AWS: autenticação, IAM, EKS, ECR, S3, RDS, Secrets Manager e VPC. Use quando: provisionar ou gerenciar recursos AWS via linha de comando, scripts de automação ou pipelines CI/CD."
user-invocable: true
---

# AWS CLI — Gerenciamento de Recursos AWS

## Quando Usar

- Provisionar ou gerenciar recursos AWS sem Terraform (scripts rápidos, bootstrap)
- Autenticar e configurar acesso a clusters EKS
- Empurrar imagens para Amazon ECR
- Gerenciar segredos no AWS Secrets Manager ou SSM Parameter Store
- Scripts de automação em Bash para pipelines CI/CD

---

## Instalação e Configuração

```bash
# Instalar AWS CLI v2
# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# macOS
brew install awscli

# Verificar
aws --version           # >= 2.15 recomendado

# Configurar credenciais (dev local)
aws configure
# AWS Access Key ID:     AKIA...
# AWS Secret Access Key: ...
# Default region name:   us-east-1
# Default output format: json

# Múltiplos profiles
aws configure --profile production
aws configure --profile staging

# Usar profile
export AWS_PROFILE=production
aws sts get-caller-identity     # verificar identidade atual

# Variáveis de ambiente (CI/CD — preferido)
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"
```

---

## IAM — Identity and Access Management

```bash
# Criar usuário IAM para CI/CD
aws iam create-user --user-name cicd-DevKit

# Criar access key
aws iam create-access-key --user-name cicd-DevKit

# Anexar policy gerenciada
aws iam attach-user-policy \
  --user-name cicd-DevKit \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

# Criar policy customizada
aws iam create-policy \
  --policy-name DevKitECRPolicy \
  --policy-document file://ecr-policy.json

# Listar roles
aws iam list-roles --output table

# Criar role para EKS
aws iam create-role \
  --role-name eksClusterRole \
  --assume-role-policy-document file://eks-trust-policy.json

# Verificar permissões efetivas
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:user/cicd-DevKit \
  --action-names "eks:DescribeCluster" "ecr:GetAuthorizationToken"
```

---

## EKS — Amazon Elastic Kubernetes Service

```bash
# Criar cluster EKS
aws eks create-cluster \
  --name eks-DevKit-prod \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/eksClusterRole \
  --resources-vpc-config subnetIds=$SUBNET_IDS,securityGroupIds=$SG_IDS \
  --kubernetes-version 1.29 \
  --region us-east-1

# Aguardar cluster ficar ativo
aws eks wait cluster-active \
  --name eks-DevKit-prod

# Criar node group (managed)
aws eks create-nodegroup \
  --cluster-name eks-DevKit-prod \
  --nodegroup-name workers \
  --node-role arn:aws:iam::$ACCOUNT_ID:role/eksNodeRole \
  --subnets $SUBNET_ID_1 $SUBNET_ID_2 \
  --instance-types t3.xlarge \
  --scaling-config minSize=2,maxSize=10,desiredSize=3 \
  --disk-size 100 \
  --ami-type AL2_x86_64

# Configurar kubeconfig
aws eks update-kubeconfig \
  --name eks-DevKit-prod \
  --region us-east-1

# Com profile específico
aws eks update-kubeconfig \
  --name eks-DevKit-prod \
  --region us-east-1 \
  --profile production

# Listar clusters
aws eks list-clusters --output table

# Descrever cluster
aws eks describe-cluster --name eks-DevKit-prod

# Listar node groups
aws eks list-nodegroups --cluster-name eks-DevKit-prod

# Atualizar versão do cluster
aws eks update-cluster-version \
  --name eks-DevKit-prod \
  --kubernetes-version 1.30

# Habilitar OIDC provider (necessário para IRSA)
eksctl utils associate-iam-oidc-provider \
  --cluster eks-DevKit-prod \
  --approve
```

---

## ECR — Amazon Elastic Container Registry

```bash
# Criar repositório
aws ecr create-repository \
  --repository-name DevKit/api \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256 \
  --region us-east-1

# Autenticar Docker no ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build e push
docker build -t DevKit/api:$GIT_SHA .
docker tag DevKit/api:$GIT_SHA \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/DevKit/api:$GIT_SHA

docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/DevKit/api:$GIT_SHA

# Listar images
aws ecr list-images \
  --repository-name DevKit/api \
  --output table

# Lifecycle policy — manter apenas 10 imagens
aws ecr put-lifecycle-policy \
  --repository-name DevKit/api \
  --lifecycle-policy-text '{
    "rules": [{
      "rulePriority": 1,
      "selection": {
        "tagStatus": "untagged",
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": { "type": "expire" }
    }]
  }'
```

---

## S3

```bash
# Criar bucket (nomes são globais — use prefixo único)
aws s3 mb s3://DevKit-assets-prod-$ACCOUNT_ID \
  --region us-east-1

# Configurar versionamento
aws s3api put-bucket-versioning \
  --bucket DevKit-assets-prod \
  --versioning-configuration Status=Enabled

# Bloquear acesso público
aws s3api put-public-access-block \
  --bucket DevKit-assets-prod \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Upload / sync
aws s3 cp ./dist s3://DevKit-assets-prod/frontend --recursive
aws s3 sync ./dist s3://DevKit-assets-prod/frontend --delete

# Download
aws s3 cp s3://DevKit-assets-prod/arquivo.txt ./

# Listar
aws s3 ls s3://DevKit-assets-prod --recursive --human-readable

# Gerar URL pré-assinada (acesso temporário)
aws s3 presign s3://DevKit-assets-prod/relatorio.pdf \
  --expires-in 3600

# Configurar lifecycle (mover para Glacier após 90 dias)
aws s3api put-bucket-lifecycle-configuration \
  --bucket DevKit-assets-prod \
  --lifecycle-configuration file://lifecycle.json
```

---

## Secrets Manager

```bash
# Criar secret
aws secretsmanager create-secret \
  --name DevKit/production/db-password \
  --description "Senha do banco de dados em produção" \
  --secret-string '{"password":"senha_segura","username":"pgadmin"}'

# Atualizar valor
aws secretsmanager update-secret \
  --secret-id DevKit/production/db-password \
  --secret-string '{"password":"nova_senha","username":"pgadmin"}'

# Ler secret
aws secretsmanager get-secret-value \
  --secret-id DevKit/production/db-password \
  --query SecretString \
  --output text

# SSM Parameter Store (strings simples)
aws ssm put-parameter \
  --name "/DevKit/production/DATABASE_URL" \
  --value "postgresql://user:pass@host:5432/db" \
  --type SecureString \
  --overwrite

aws ssm get-parameter \
  --name "/DevKit/production/DATABASE_URL" \
  --with-decryption \
  --query Parameter.Value \
  --output text

# Listar parâmetros por path
aws ssm get-parameters-by-path \
  --path "/DevKit/production" \
  --recursive \
  --with-decryption
```

---

## VPC e Networking

```bash
# Criar VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=vpc-DevKit-prod}]'

# Criar subnets (multi-AZ para EKS)
aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=subnet-private-1a},{Key=kubernetes.io/role/internal-elb,Value=1}]'

# Security Group para EKS
aws ec2 create-security-group \
  --group-name sg-eks-nodes \
  --description "Security group para nodes EKS" \
  --vpc-id $VPC_ID

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

---

## Consultas Úteis

```bash
# Listar todas as instâncias EC2 em running
aws ec2 describe-instances \
  --filters Name=instance-state-name,Values=running \
  --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value|[0],PublicIpAddress]' \
  --output table

# Account ID atual
aws sts get-caller-identity --query Account --output text

# Região atual
aws configure get region

# Preço spot de instâncias
aws ec2 describe-spot-price-history \
  --instance-types t3.xlarge \
  --product-descriptions "Linux/UNIX" \
  --start-time $(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --output table
```

---

## Output Esperado

1. Credenciais e profiles configurados para os ambientes
2. Cluster EKS com kubeconfig atualizado
3. ECR com lifecycle policy e Docker autenticado
4. Secrets Manager com segredos da aplicação
5. Comandos documentados para operações recorrentes
