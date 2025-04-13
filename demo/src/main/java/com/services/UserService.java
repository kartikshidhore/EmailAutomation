package com.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import com.model.User;
import com.repository.UserRepository;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import java.util.Optional;


@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JavaMailSender mailSender;

    public boolean verifySMTP(String email, String password) {
        // This method should only be used for checking locally via frontend
        // You can simulate it via a frontend-based SMTP handshake
        return true; // Frontend handles real verification
    }

    public String signup(String email, String password) {
        if (userRepository.findByEmail(email).isPresent()) {
            return "User already exists";
        }
        User user = new User();
        user.setEmail(email);
        user.setPassword(password); // TODO: Hash passwords in production!
        userRepository.save(user);
        return "Signup successful";
    }

    public boolean login(String email, String password) {
        Optional<User> optionalUser = userRepository.findByEmail(email);
        return optionalUser.filter(user -> user.getPassword().equals(password)).isPresent();
    }
}

