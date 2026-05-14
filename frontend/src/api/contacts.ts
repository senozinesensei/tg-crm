import client from './client'

export async function getContacts(search = '') {
  const res = await client.get('/contacts', { params: { search } })
  return res.data
}

export async function getContact(contactId: string) {
  const res = await client.get(`/contacts/${contactId}`)
  return res.data
}
