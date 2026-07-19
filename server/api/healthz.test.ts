import { describe, expect, it } from 'vitest'

import healthHandler, { nuxtHealthResponse } from './healthz.get'

describe('Nuxt health endpoint', () => {
  it('returns only the stable Nuxt health contract', () => {
    expect(healthHandler({} as never)).toEqual({
      status: 'ok',
      service: 'nuxt',
    })
    expect(Object.keys(nuxtHealthResponse).sort()).toEqual(['service', 'status'])
  })

  it('has no backend or secret-bearing fields', () => {
    const serialized = JSON.stringify(nuxtHealthResponse).toLowerCase()
    expect(serialized).not.toMatch(/django|postgres|secret|token|password|key/)
  })
})
