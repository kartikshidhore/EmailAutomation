package com.example.demo.service;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import com.example.demo.security.JwtUtil;
import jakarta.mail.Session;
import jakarta.mail.Transport;
import jakarta.mail.PasswordAuthentication;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.Properties;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    public String signup(String email, String smtpPassword) {
        if (userRepository.findByEmail(email).isPresent()) {
            return "User already exists";
        }

        if (!verifySMTP(email, smtpPassword)) {
            return "SMTP verification failed.";
        }

        User user = new User();
        user.setEmail(email);
        user.setSmtpPassword(smtpPassword);
        userRepository.save(user);

        return "Signup successful";
    }

    public String login(String email, String smtpPassword) {
        Optional<User> optionalUser = userRepository.findByEmail(email);
        if (optionalUser.isPresent() && optionalUser.get().getSmtpPassword().equals(smtpPassword)) {
            return jwtUtil.generateToken(email); // generate JWT token
        }
        return null;
    }

    private boolean verifySMTP(String email, String password) {
        try {
            Properties props = new Properties();
            props.put("mail.smtp.auth", "true");
            props.put("mail.smtp.starttls.enable", "true");
            props.put("mail.smtp.host", "smtp.gmail.com");
            props.put("mail.smtp.port", "587");

            Session session = Session.getInstance(props,
                    new jakarta.mail.Authenticator() {
                        protected PasswordAuthentication getPasswordAuthentication() {
                            return new PasswordAuthentication(email, password);
                        }
                    });

            Transport transport = session.getTransport("smtp");
            transport.connect();
            transport.close();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}

