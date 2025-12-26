# DigitalOcean Kubernetes (DOKS) Infrastructure
# Phase V: Advanced Cloud Deployment
# Author: Sharmeen Asif

terraform {
  required_version = ">= 1.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Configure DigitalOcean provider
provider "digitalocean" {
  token = var.do_token
}

# Create Kubernetes cluster
resource "digitalocean_kubernetes_cluster" "todo_cluster" {
  name    = "todo-app-cluster"
  region  = var.region
  version = var.kubernetes_version

  node_pool {
    name       = "worker-pool"
    size       = "s-2vcpu-4gb"
    node_count = 3
    auto_scale = true
    min_nodes  = 2
    max_nodes  = 5
  }

  tags = ["todo-app", "production"]
}

# Create PostgreSQL database
resource "digitalocean_database_cluster" "postgres" {
  name       = "todo-postgres"
  engine     = "pg"
  version    = "16"
  size       = "db-s-1vcpu-1gb"
  region     = var.region
  node_count = 1

  tags = ["todo-app", "database"]
}

# Create database
resource "digitalocean_database_db" "todo_db" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "todo_db"
}

# Create database user
resource "digitalocean_database_user" "todo_user" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "todo_user"
}

# Create Load Balancer
resource "digitalocean_loadbalancer" "public" {
  name   = "todo-app-lb"
  region = var.region

  forwarding_rule {
    entry_port     = 443
    entry_protocol = "https"

    target_port     = 80
    target_protocol = "http"

    tls_passthrough = false
  }

  forwarding_rule {
    entry_port     = 80
    entry_protocol = "http"

    target_port     = 80
    target_protocol = "http"
  }

  healthcheck {
    port     = 80
    protocol = "http"
    path     = "/"
  }

  droplet_tag = "todo-app"
}

# Outputs
output "cluster_id" {
  value = digitalocean_kubernetes_cluster.todo_cluster.id
}

output "cluster_endpoint" {
  value = digitalocean_kubernetes_cluster.todo_cluster.endpoint
}

output "database_uri" {
  value     = digitalocean_database_cluster.postgres.uri
  sensitive = true
}

output "loadbalancer_ip" {
  value = digitalocean_loadbalancer.public.ip
}
