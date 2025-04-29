package com.example.demo.service;

import com.example.demo.model.User;
import com.example.demo.model.EmailRequest;
import com.example.demo.repository.UserRepository;
import jakarta.mail.*;
import jakarta.mail.internet.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Properties;

@Service
public class EmailService {

    @Autowired
    private UserRepository userRepository;

    public boolean sendEmails(String userEmail, EmailRequest request) {
        try {
            // Fetch the logged-in user from database
            User user = userRepository.findByEmail(userEmail)
                    .orElseThrow(() -> new RuntimeException("User not found."));

            String senderEmail = user.getEmail();
            String senderPassword = user.getSmtpPassword(); // Use saved SMTP password

            Properties props = new Properties();
            props.put("mail.smtp.auth", "true");
            props.put("mail.smtp.starttls.enable", "true");
            props.put("mail.smtp.host", "smtp.gmail.com");
            props.put("mail.smtp.port", "587");

            Session session = Session.getInstance(props, new Authenticator() {
                protected PasswordAuthentication getPasswordAuthentication() {
                    return new PasswordAuthentication(senderEmail, senderPassword);
                }
            });

            // Loop through each recipient and send email
            for (var recipient : request.getRecipients()) {
                MimeMessage message = new MimeMessage(session);
                message.setFrom(new InternetAddress(senderEmail));
                message.addRecipient(Message.RecipientType.TO, new InternetAddress(recipient.getEmail()));
                message.setSubject(request.getSubject());

                MimeBodyPart mimeBodyPart = new MimeBodyPart();
                mimeBodyPart.setContent(request.getBody(), "text/html");

                Multipart multipart = new MimeMultipart();
                multipart.addBodyPart(mimeBodyPart);

                // Attach files
                if (request.getAttachments() != null) {
                    for (var attachment : request.getAttachments()) {
                        MimeBodyPart attachmentPart = new MimeBodyPart();
                        attachmentPart.setFileName(attachment.getFilename());
                        attachmentPart.setContent(hexStringToByteArray(attachment.getFiledata()), "application/octet-stream");
                        multipart.addBodyPart(attachmentPart);
                    }
                }

                message.setContent(multipart);
                Transport.send(message);
            }

            return true;

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    private byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                                 + Character.digit(s.charAt(i+1), 16));
        }
        return data;
    }
}

