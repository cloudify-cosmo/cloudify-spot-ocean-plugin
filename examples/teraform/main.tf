provider "kubernetes" {
  config_path = "~/.kube/config"
}

module "ocean-controller" {
  source = "spotinst/ocean-controller/spotinst"

  # Credentials.
  spotinst_token   = var.spot_token
  spotinst_account = var.spot_account

  # Configuration.
  cluster_identifier = var.eks_name
}

