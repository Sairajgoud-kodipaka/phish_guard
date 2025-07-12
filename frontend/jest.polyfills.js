// Jest polyfills for missing browser APIs
import { TextEncoder, TextDecoder } from 'util'

global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

// Mock structuredClone if not available
global.structuredClone = global.structuredClone || ((val) => JSON.parse(JSON.stringify(val)))

// Mock crypto.randomUUID
global.crypto = global.crypto || {}
global.crypto.randomUUID = global.crypto.randomUUID || (() => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
})

// Mock URL.createObjectURL
global.URL.createObjectURL = global.URL.createObjectURL || (() => 'mock-url')
global.URL.revokeObjectURL = global.URL.revokeObjectURL || (() => {}) 