#!/bin/bash
set -x

service txos start
ssh tt-peer-controller. "/sbin/service txos start"

