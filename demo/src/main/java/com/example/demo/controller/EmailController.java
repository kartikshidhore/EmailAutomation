package com.example.demo.controller;

import com.example.demo.model.EmailRequest;
import com.example.demo.service.EmailService;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/private")
public class EmailController {

    @Autowired
    private EmailService emailService;

    @PostMapping("/send-emails")
    public ResponseEntity<?> sendEmails(@RequestBody EmailRequest request) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String userEmail = authentication.getName(); // from JWT token

        boolean success = emailService.sendEmails(userEmail, request);
        if (success) {
            return ResponseEntity.ok(Map.of("status", "success", "message", "Emails sent successfully"));
        } else {
            return ResponseEntity.badRequest().body(Map.of("status", "fail", "message", "Failed to send emails"));
        }
    }
}
