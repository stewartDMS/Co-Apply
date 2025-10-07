"""
Desktop Autofill Helper using Playwright
Automates form filling on job application websites
"""

import asyncio
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Page, Browser
import json
import os


class FormFieldMapping:
    """Common field mappings for job applications"""
    
    # Common field name patterns
    FIELD_PATTERNS = {
        'first_name': ['firstname', 'first_name', 'fname', 'given_name', 'forename'],
        'last_name': ['lastname', 'last_name', 'lname', 'surname', 'family_name'],
        'full_name': ['fullname', 'full_name', 'name', 'applicant_name'],
        'email': ['email', 'e-mail', 'email_address', 'emailaddress'],
        'phone': ['phone', 'telephone', 'mobile', 'phone_number', 'phonenumber', 'tel'],
        'address': ['address', 'street', 'address_line'],
        'city': ['city', 'town'],
        'state': ['state', 'province', 'region'],
        'zip': ['zip', 'zipcode', 'postal', 'postcode', 'postal_code'],
        'country': ['country'],
        'linkedin': ['linkedin', 'linkedin_url', 'linkedin_profile'],
        'github': ['github', 'github_url', 'github_profile'],
        'website': ['website', 'portfolio', 'personal_website', 'url'],
        'cover_letter': ['cover_letter', 'coverletter', 'cover', 'motivation'],
        'resume': ['resume', 'cv', 'curriculum_vitae'],
        'years_experience': ['experience', 'years_experience', 'yearsofexperience'],
        'current_company': ['current_company', 'employer', 'company'],
        'current_title': ['current_title', 'job_title', 'position'],
    }


class JobApplicationAutofill:
    """Automates job application form filling"""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def start(self):
        """Start the browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def close(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()

    async def navigate_to_url(self, url: str):
        """Navigate to a job application URL"""
        await self.page.goto(url)
        await self.page.wait_for_load_state('networkidle')

    async def detect_fields(self) -> List[Dict[str, str]]:
        """Detect form fields on the current page"""
        fields = []
        
        # Detect input fields
        inputs = await self.page.query_selector_all('input')
        for input_elem in inputs:
            input_type = await input_elem.get_attribute('type')
            if input_type in ['text', 'email', 'tel', 'url', None]:
                name = await input_elem.get_attribute('name')
                id_attr = await input_elem.get_attribute('id')
                placeholder = await input_elem.get_attribute('placeholder')
                
                fields.append({
                    'type': 'input',
                    'input_type': input_type or 'text',
                    'name': name,
                    'id': id_attr,
                    'placeholder': placeholder,
                })
        
        # Detect textarea fields
        textareas = await self.page.query_selector_all('textarea')
        for textarea in textareas:
            name = await textarea.get_attribute('name')
            id_attr = await textarea.get_attribute('id')
            placeholder = await textarea.get_attribute('placeholder')
            
            fields.append({
                'type': 'textarea',
                'name': name,
                'id': id_attr,
                'placeholder': placeholder,
            })
        
        # Detect file inputs
        file_inputs = await self.page.query_selector_all('input[type="file"]')
        for file_input in file_inputs:
            name = await file_input.get_attribute('name')
            id_attr = await file_input.get_attribute('id')
            
            fields.append({
                'type': 'file',
                'name': name,
                'id': id_attr,
            })
        
        return fields

    def map_profile_to_fields(self, profile_data: Dict[str, str], 
                             detected_fields: List[Dict[str, str]]) -> Dict[str, str]:
        """Map profile data to detected form fields"""
        field_map = {}
        
        for field in detected_fields:
            field_identifier = field.get('name') or field.get('id') or ''
            field_identifier_lower = field_identifier.lower()
            
            # Check against known patterns
            for data_key, patterns in FormFieldMapping.FIELD_PATTERNS.items():
                if data_key in profile_data:
                    for pattern in patterns:
                        if pattern in field_identifier_lower:
                            field_map[field_identifier] = profile_data[data_key]
                            break
        
        return field_map

    async def fill_form(self, field_values: Dict[str, str], file_uploads: Dict[str, str] = None):
        """Fill form fields with provided values"""
        filled_count = 0
        
        for field_identifier, value in field_values.items():
            try:
                # Try by name first
                selector = f'[name="{field_identifier}"]'
                element = await self.page.query_selector(selector)
                
                # Try by id if not found
                if not element:
                    selector = f'#{field_identifier}'
                    element = await self.page.query_selector(selector)
                
                if element:
                    await element.fill(value)
                    filled_count += 1
            except Exception as e:
                print(f"Failed to fill field {field_identifier}: {e}")
        
        # Handle file uploads
        if file_uploads:
            for field_identifier, file_path in file_uploads.items():
                try:
                    selector = f'input[type="file"][name="{field_identifier}"]'
                    element = await self.page.query_selector(selector)
                    
                    if not element:
                        selector = f'input[type="file"]#{field_identifier}'
                        element = await self.page.query_selector(selector)
                    
                    if element and os.path.exists(file_path):
                        await element.set_input_files(file_path)
                        filled_count += 1
                except Exception as e:
                    print(f"Failed to upload file for {field_identifier}: {e}")
        
        return filled_count

    async def take_screenshot(self, filepath: str):
        """Take a screenshot of the current page"""
        await self.page.screenshot(path=filepath, full_page=True)

    async def wait_for_manual_action(self, message: str = "Waiting for manual action..."):
        """Pause and wait for manual user action (e.g., captcha)"""
        print(message)
        print("Press Enter in the console when ready to continue...")
        # In a real implementation, this would need a proper way to pause

    async def click_element(self, selector: str):
        """Click an element (e.g., submit button)"""
        await self.page.click(selector)

    async def save_application_state(self, filepath: str):
        """Save the current state for resuming later"""
        state = {
            'url': self.page.url,
            'cookies': await self.page.context.cookies(),
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    async def restore_application_state(self, filepath: str):
        """Restore a saved application state"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        await self.page.context.add_cookies(state['cookies'])
        await self.page.goto(state['url'])

    async def auto_apply(self, url: str, profile_data: Dict[str, str], 
                        file_uploads: Dict[str, str] = None,
                        submit: bool = False) -> Dict[str, any]:
        """
        Automatically fill a job application form
        
        Args:
            url: Job application URL
            profile_data: User profile data
            file_uploads: File paths for resume, cover letter, etc.
            submit: Whether to auto-submit (False for safety)
            
        Returns:
            Result dict with status and details
        """
        try:
            # Navigate to the page
            await self.navigate_to_url(url)
            
            # Detect fields
            detected_fields = await self.detect_fields()
            
            # Map profile data to fields
            field_mapping = self.map_profile_to_fields(profile_data, detected_fields)
            
            # Fill the form
            filled_count = await self.fill_form(field_mapping, file_uploads)
            
            # Take screenshot for verification
            screenshot_path = f"/tmp/application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await self.take_screenshot(screenshot_path)
            
            result = {
                'success': True,
                'url': url,
                'fields_detected': len(detected_fields),
                'fields_filled': filled_count,
                'screenshot': screenshot_path,
                'submitted': False,
            }
            
            # Optionally submit
            if submit:
                # Look for submit button (common patterns)
                submit_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Submit")',
                    'button:has-text("Apply")',
                ]
                
                for selector in submit_selectors:
                    try:
                        await self.click_element(selector)
                        result['submitted'] = True
                        break
                    except:
                        continue
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url,
            }


# Helper function for synchronous usage
def autofill_application(url: str, profile_data: Dict[str, str],
                        file_uploads: Dict[str, str] = None,
                        headless: bool = False) -> Dict[str, any]:
    """
    Synchronous wrapper for auto-filling applications
    
    Args:
        url: Job application URL
        profile_data: User profile data
        file_uploads: File paths for documents
        headless: Run browser in headless mode
        
    Returns:
        Result dictionary
    """
    async def run():
        autofill = JobApplicationAutofill(headless=headless)
        await autofill.start()
        try:
            result = await autofill.auto_apply(url, profile_data, file_uploads)
            return result
        finally:
            await autofill.close()
    
    return asyncio.run(run())


# Import datetime for screenshot names
from datetime import datetime
