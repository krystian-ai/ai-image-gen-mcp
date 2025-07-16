## Technical Clarifications for PRD

**Date:** 2025-01-16  
**Subject:** GPT-Image-1 API Implementation Details

### Overview

Based on implementation research and OpenAI documentation review, the following technical clarifications should be considered for the MCP Image Generation Server MVP.

### GPT-Image-1 API Details

1. **API Endpoint**
   - Uses OpenAI's Responses API (`/v1/responses`) instead of the traditional Images API (`/v1/images/generations`)
   - This is a multimodal endpoint that supports both text and image generation

2. **Request Format**
   ```python
   response = await client.responses.create(
       model="gpt-4.1-mini",
       input="<prompt text>",
       tools=[{"type": "image_generation"}],
   )
   ```

3. **Response Format**
   - Returns base64-encoded images in the response output
   - Images need to be decoded from base64 before storage
   - No direct URL generation - requires intermediate storage

4. **Parameter Limitations**
   - No direct support for `size`, `quality`, or `style` parameters
   - Only supports `n=1` (single image generation per request)
   - Maximum prompt length: 4000 characters
   - Model selection affects quality/style implicitly

### Architecture Updates

1. **Model Router Implementation**
   - Uses Python SDK calls (OpenAI AsyncClient) rather than REST/gRPC
   - Simplified error handling through SDK abstractions
   - Async/await patterns throughout

2. **Storage Strategy**
   - MVP implements local filesystem storage
   - Generated images saved with metadata JSON files
   - Future migration path to S3/GCS maintained through storage interface

3. **Response Flow**
   - Server receives base64 image data
   - Decodes and saves to local storage
   - Returns file paths (not URLs) in MVP
   - Future versions will implement signed URL generation

### Recommendations

1. **PRD Updates**
   - Update architecture diagram to show SDK-based integration
   - Clarify that MVP returns file paths, not URLs
   - Note GPT-Image-1 parameter limitations

2. **Future Considerations**
   - DALL-E 3 integration will use different API (`/v1/images/generations`)
   - DALL-E 3 supports size, quality, and style parameters
   - Consider unified parameter mapping layer in Model Router

3. **Migration Path**
   - Current local storage design allows easy migration to cloud storage
   - StorageBackend interface supports future S3/GCS implementations
   - Consider implementing URL generation even for local files (file:// URLs)