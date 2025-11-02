import dotenv from 'dotenv';

dotenv.config({
    path: '.env'
})

export const { RABBITMQ_URL, NODEMAILER_KEY } = process.env