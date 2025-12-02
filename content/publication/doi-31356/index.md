---
title: 'The Long Road to Trajectory Privacy: Differential Privacy and Generative Models'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Erik Buchholz

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2025-07-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2025-12-02T00:23:55.740193Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- thesis

# Publication name and optional abbreviated publication name.
publication: ''
publication_short: ''

doi: 10.26190/unsworks/31356

abstract: Location trajectories represent a valuable resource for location-based services
  and analyses, enabling applications ranging from public transport optimisation to
  disease spread modelling. However, trajectories also reveal sensitive information,
  such as political or religious affiliations, necessitating privacy-preserving mechanisms
  for their publication. This thesis seeks to advance privacy-preserving trajectory
  publication by balancing high utility with formal privacy guarantees. As our first
  contribution, we introduce a novel framework based on five design goals – formal
  guarantees, unit of privacy, empirical privacy, utility, and practicality – enabling
  a fair and systematic evaluation of existing methods and guiding the design of new
  mechanisms. Second, applying this framework, we comprehensively evaluate related
  work and demonstrate that no existing mechanism satisfies all goals. Third, we propose
  the first deep learning-based reconstruction attack capable of partially recovering
  trajectories protected by differentially private (DP) mechanisms, reducing spatial
  distance metrics by over 68% for mechanisms with ε ≤ 1. The attack remains effective
  when transferring from one dataset to another, highlighting the limitations of state-of-the-art
  (SOTA) protection mechanisms. Synthetic data generation using deep learning has
  emerged as an alternative to conventional trajectory protection. As our fourth contribution,
  we provide a systematic review and experimental evaluation of synthetic trajectory
  generation methods, revealing improved utility but a lack of formal privacy guarantees.
  Our practical evaluations underline the risk of privacy leakage in these SOTA models.
  Fifth, we conduct a large-scale empirical study evaluating six generative models
  from other domains, identifying their inability to replicate spatial distributions
  and underscoring the necessity of domain-specific adaptations. Sixth, we propose
  a novel transformation algorithm enabling the effective use of CNN-based generative
  models for trajectory generation, outperforming recurrent models regarding spatial
  distribution quality, e.g., reducing the sliced Wasserstein distance (SWD) by 25%-73%
  on the considered datasets compared to a recurrent baseline. Seventh, we quantify
  and improve the utility cost of differential privacy in synthetic trajectory generation
  in three steps. (1) We evaluate several models with and without DP-SGD, the most
  common method for achieving DP guarantees in deep learning, quantifying the significant
  utility loss incurred for trajectory generation. (2) We propose a novel DP conditional
  information mechanism that enhances training stability, especially when combined
  with DP-SGD, for unstable models, and on smaller datasets. On the GeoLife dataset,
  the mechanism decreases the SWD by 41%-61% compared to an unconditional model under
  DP-SGD. (3) We evaluate the impact of the model type on the utility by comparing
  a GAN, a VAE, and a diffusion model with similar architectures, both with and without
  guarantees. The best non-DP model does not necessarily perform best when guarantees
  are provided, as the GAN outperforms the SOTA diffusion model by 6%-64% regarding
  SWD on two datasets when providing full DP guarantees. Overall, this thesis contributes
  to privacy-preserving trajectory publication by introducing a comprehensive evaluation
  framework, exposing limitations in existing methods, and demonstrating the potential
  of synthetic trajectory generation.

# Summary. An optional shortened abstract.
summary: ''

tags: []

# Display this page in a list of Featured pages?
featured: false

# Links
url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

# Publication image
# Add an image named `featured.jpg/png` to your page's folder then add a caption below.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ['internal-project']` links to `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []
links:
- name: URL
  url: https://doi.org/10.26190/UNSWORKS/31356
---
