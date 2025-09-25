---
title: "{{ slicestr .URL (sub (len .URL) 5) (sub (len .URL) 1) }} Seminar - AGNT @ UofSC"
description: "Talk and schedule information for a seminar of the Algebra, Geometry, and Number Theory group at the Univesity of South Carolina"
layout: yearly
draft: false
katex: true
nav: Team
categories:
- Seminar 
tags:
- Research # research, learning, ... 
---
{{- $len := len (.URL) -}}
{{<center>}}
## {{ slicestr .URL (sub $len 5) (sub $len 1) }} Seminar Schedule
{{</center>}}

--------------

<!-- Seminar description and information goes here. Talk information will be populated below. -->