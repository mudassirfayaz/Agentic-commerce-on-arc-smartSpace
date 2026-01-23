## 1. CSS Fixes
- [x] 1.1 Remove duplicate `position: relative;` declaration from `.chatbot-toggle` class in `Chatbot.css`
- [x] 1.2 Increase `.chatbot-toggle` z-index from `1000` to `1100` (or higher) to ensure it appears above header (`z-index: 1020`)
- [x] 1.3 Verify `.chatbot-window` z-index is appropriate (should be `1099` or similar, below toggle button but above header)
- [x] 1.4 Test that chatbot icon is visible in right-bottom corner on both landing page and dashboard pages
- [x] 1.5 Verify chatbot icon is not hidden under header when scrolling
- [x] 1.6 Test responsive behavior on mobile devices to ensure icon remains accessible

## 2. Validation
- [x] 2.1 Visual inspection: Chatbot icon visible in right-bottom corner
- [x] 2.2 Test scrolling: Icon remains visible and accessible when header is sticky
- [x] 2.3 Test on different viewport sizes (desktop, tablet, mobile)
- [x] 2.4 Verify icon appears above all other UI elements including header

