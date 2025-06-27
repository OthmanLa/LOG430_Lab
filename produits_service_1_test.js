import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 10 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    errors: ['rate<0.1'],
    http_req_duration: ['p(95)<500'],
  },
};

const BASE_URL = 'http://localhost:8016/api/v1';

const AUTH = {
  headers: {
    'Authorization': 'token1',
    'Content-Type': 'application/json',
  },
};

export default function () {
  let res = http.get(`${BASE_URL}/products`, AUTH);
  check(res, { 'produits-service-1 200': r => r.status === 200 }) || errorRate.add(1);
  sleep(1);
}
