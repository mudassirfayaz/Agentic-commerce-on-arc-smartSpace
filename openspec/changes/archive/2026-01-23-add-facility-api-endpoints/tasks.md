## 1. Model Resolution Service
- [x] 1.1 Create model resolver service
  - Create `backend/src/services/model_resolver.py`
  - Implement model name parsing (`{provider}/{model}` format)
  - Add provider/model validation
  - Support provider/model mapping lookup
  - Handle invalid model names with clear error messages
- [x] 1.2 Add provider/model registry
  - Create configuration for supported providers and models
  - Support Ollama models (qalb-urdu, deepseek-r1, llama2)
  - Support OpenAI models (gpt-4, tts-1, etc.)
  - Support Anthropic models (claude-3, etc.)
  - Make registry easily extensible

## 2. Request Transformation Layer
- [x] 2.1 Create request transformers module
  - Create `backend/src/utils/request_transformers.py`
  - Implement base transformer interface
  - Create text completion transformer
  - Create audio/speech transformer
  - Create image generation transformer
  - Create embeddings transformer
  - Create vision transformer
- [x] 2.2 Implement transformation logic
  - Map facility-specific format to agentic brain format
  - Extract operation_type from facility
  - Handle facility-specific parameters
  - Preserve metadata and optional fields
  - Validate required fields per facility

## 3. Facility Controller
- [x] 3.1 Create facility controller
  - Create `backend/src/controllers/facility_controller.py`
  - Implement request handling for each facility type
  - Integrate model resolver
  - Integrate request transformers
  - Call agentic service
  - Transform response back to facility format
- [x] 3.2 Add error handling
  - Handle invalid model names
  - Handle missing required fields
  - Handle agentic brain errors
  - Return user-friendly error messages
  - Maintain proper HTTP status codes

## 4. Facility-Specific Routes
- [x] 4.1 Create text completion route
  - Create `backend/src/routes/v1/text.py`
  - Implement `POST /v1/text/completion` endpoint
  - Add Pydantic model for text completion request
  - Integrate API key authentication
  - Connect to facility controller
- [x] 4.2 Create audio/speech route
  - Create `backend/src/routes/v1/audio.py`
  - Implement `POST /v1/audio/speech` endpoint
  - Add Pydantic model for audio request
  - Integrate API key authentication
  - Connect to facility controller
- [x] 4.3 Create image generation route
  - Create `backend/src/routes/v1/images.py`
  - Implement `POST /v1/images/generate` endpoint
  - Add Pydantic model for image request
  - Integrate API key authentication
  - Connect to facility controller
- [x] 4.4 Create embeddings route
  - Create `backend/src/routes/v1/embeddings.py`
  - Implement `POST /v1/embeddings` endpoint
  - Add Pydantic model for embeddings request
  - Integrate API key authentication
  - Connect to facility controller
- [x] 4.5 Create vision route
  - Create `backend/src/routes/v1/vision.py`
  - Implement `POST /v1/vision/analyze` endpoint
  - Add Pydantic model for vision request
  - Integrate API key authentication
  - Connect to facility controller

## 5. Route Registration
- [x] 5.1 Register new routes in app
  - Update `backend/app.py` to include new facility routes
  - Ensure routes are mounted at root level (`/v1/...`) not `/api/v1/...`
  - Add route tags for API documentation
  - Verify CORS configuration works for new routes

## 6. Request Validation
- [x] 6.1 Add Pydantic models for each facility
  - Text completion request model
  - Audio/speech request model
  - Image generation request model
  - Embeddings request model
  - Vision request model
- [x] 6.2 Implement validation logic
  - Validate required fields per facility
  - Validate model name format
  - Validate parameter ranges (e.g., temperature 0-2)
  - Validate file/image formats where applicable
  - Return clear validation error messages

## 7. Response Formatting
- [x] 7.1 Transform agentic brain response
  - Extract provider response from agentic result
  - Format response to match facility-specific format
  - Include decision metadata (if needed)
  - Include payment information (if needed)
  - Handle error responses appropriately
- [x] 7.2 Add response models
  - Create Pydantic response models for each facility
  - Ensure consistent response structure
  - Include success/error indicators

## 8. Integration Testing
- [ ] 8.1 Test text completion endpoint
  - Test with valid request
  - Test with invalid API key
  - Test with invalid model name
  - Test with missing required fields
  - Verify end-to-end flow works
- [ ] 8.2 Test audio/speech endpoint
  - Test with valid request
  - Test error cases
  - Verify end-to-end flow works
- [ ] 8.3 Test image generation endpoint
  - Test with valid request
  - Test error cases
  - Verify end-to-end flow works
- [ ] 8.4 Test embeddings endpoint
  - Test with valid request
  - Test error cases
  - Verify end-to-end flow works
- [ ] 8.5 Test vision endpoint
  - Test with valid request
  - Test error cases
  - Verify end-to-end flow works

## 9. Documentation
- [ ] 9.1 Update API documentation
  - Add OpenAPI/Swagger documentation for new endpoints
  - Document request/response formats
  - Document authentication requirements
  - Add example requests for each facility
  - Document error responses
- [ ] 9.2 Update README
  - Document new endpoint structure
  - Add usage examples
  - Update architecture diagrams if needed

## 10. Optional: Frontend Integration
- [ ] 10.1 Update ApiCallInterface component (if needed)
  - Update to use new facility-specific endpoints
  - Add facility selection dropdown
  - Update request format
  - Test integration

