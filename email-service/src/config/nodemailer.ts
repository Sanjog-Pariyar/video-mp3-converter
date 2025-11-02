import nodemailer from 'nodemailer';
import { NODEMAILER_KEY } from './env.ts';

export const accountEmail = 'sanjogpariyar17@gmail.com';

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: accountEmail,
    pass: NODEMAILER_KEY
  }
})

export default transporter;