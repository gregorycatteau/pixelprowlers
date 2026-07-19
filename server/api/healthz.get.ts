import { defineEventHandler } from 'h3'

export const nuxtHealthResponse = Object.freeze({
  status: 'ok',
  service: 'nuxt',
})

export default defineEventHandler(() => nuxtHealthResponse)
