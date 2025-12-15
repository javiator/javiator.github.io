Create a new blog post for an EXISTING evolutionary project with the following requirements:

make relevant information from existing posts and setup if not provided correcly

**Post Details:**
- Title: Tenant Management Application - Deploy to Cloud (multiple approaches)
- Date: 10th Dec
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [intermediate]

**Evolutionary Project Fields:**
- project: "[Tenant Management Evolution]"
- project_type: "evolutionary"
- evolution: "Evolution [6]: [Tenant Management Application - Deploy to Cloud (multiple approaches)]"
- evolution_number: [6]
- evolution_focus: "[Tenant Management Application - Deploy to Cloud (multiple approaches)]"

**Content Requirements:**
- browse through the tenant-management-java-app application project that provides backend api for tenant management
- browse existing posts to understand how various posts have been created and especially the ones based on evolution of tenant management application
- write a engaging post showcasing the deployment to cloud of tenant management application using multiple approaches
- highlight the pros and cons of each approach
- use confluence mcp to find various approach details that have been used under page Tenant+Management+App+-+Cloud+Deployment+Experiments (page id -48332802) and all its child pages
- use refer to architecture diagram of approaches here - ../../tenant-management/tenant-management-java-app/generated-diagrams/
- the url to the post should not have any spaces
- this is the last post for this evolution - close update the status accordingly everywhere relevant

- Write engaging, informative content
- Include evolution context at the beginning
- Add proper headings and structure
- Include code examples if relevant
- Add evolution navigation components
- Make this post and the previous one as the featured post on home page

**Post Structure:**
- Introduction paragraph
- Evolution context block (using include)
- Main content with proper headings
- Code examples (if applicable)
- Key takeaways section
- Evolution posts component
- Post navigation component
- Conclusion

**Required Updates:**
1. **Update Project Hub:**
   - Add new post to the project overview in `_pages/projects/[project-name]/index.md`
   - Update post count and current status

2. **Update Evolution Page:**
   - Add new post to the specific evolution page in `_pages/projects/[project-name]/evolution-[X]/index.md`
   - Update post list and description

3. **Update Posts Timeline:**
   - Add new post to chronological timeline in `_pages/projects/[project-name]/posts/index.md`
   - Update post count and evolution summary

4. **Update Homepage:**
   - Update featured project section if this is the current active evolution
   - Update post count and status

5. **Update Evolution Navigation:**
   - Ensure cross-evolution links work correctly
   - Update evolution status if this completes an evolution

**File Location:**
- Create in `_posts/` directory with proper naming convention: `YYYY-MM-DD-post-title.md`

**Include Components:**
- Add `{% include evolution/post-navigation.html %}` at the end
- Add `{% include evolution/evolution-posts.html %}` before post navigation

**Cross-References:**
- Link to related posts in the same evolution
- Link to previous/next evolutions where appropriate
- Link back to project hub and evolution pages