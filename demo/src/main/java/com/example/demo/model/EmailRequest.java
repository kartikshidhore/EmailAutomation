package com.example.demo.model;

import java.util.List;

public class EmailRequest {
    private String subject;
    private String body;
    private List<Recipient> recipients;
    private List<Attachment> attachments;

    // Main class getters/setters
    public String getSubject() {
        return subject;
    }
    public void setSubject(String subject) {
        this.subject = subject;
    }

    public String getBody() {
        return body;
    }
    public void setBody(String body) {
        this.body = body;
    }

    public List<Recipient> getRecipients() {
        return recipients;
    }
    public void setRecipients(List<Recipient> recipients) {
        this.recipients = recipients;
    }

    public List<Attachment> getAttachments() {
        return attachments;
    }
    public void setAttachments(List<Attachment> attachments) {
        this.attachments = attachments;
    }

    // ✅ Nested static class for Recipients
    public static class Recipient {
        private String name;
        private String email;

        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }

        public String getEmail() {
            return email;
        }
        public void setEmail(String email) {
            this.email = email;
        }
    }

    //Nested static class for Attachments
    public static class Attachment {
        private String filename;
        private String filedata;  // hex string

        public String getFilename() {
            return filename;
        }
        public void setFilename(String filename) {
            this.filename = filename;
        }

        public String getFiledata() {
            return filedata;
        }
        public void setFiledata(String filedata) {
            this.filedata = filedata;
        }
    }
}