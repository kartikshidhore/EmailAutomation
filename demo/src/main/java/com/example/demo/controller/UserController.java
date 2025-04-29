package com.example.demo.controller;

import com.example.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/auth")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/signup")
    public ResponseEntity<?> signup(@RequestBody Map<String, String> signupData) {
        String email = signupData.get("email");
        String password = signupData.get("password");

        String result = userService.signup(email, password);
        if (result.equals("Signup successful")) {
            return ResponseEntity.ok(Map.of("status", "success", "message", result));
        } else {
            return ResponseEntity.badRequest().body(Map.of("status", "fail", "message", result));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> loginData) {
        String email = loginData.get("email");
        String password = loginData.get("password");

        String token = userService.login(email, password);
        if (token != null) {
            return ResponseEntity.ok(Map.of("status", "success", "token", token));
        } else {
            return ResponseEntity.badRequest().body(Map.of("status", "fail", "message", "Invalid credentials"));
        }
    }
}
