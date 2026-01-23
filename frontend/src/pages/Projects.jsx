import DashboardLayout from '../components/Dashboard/DashboardLayout'
import './Projects.css'

const Projects = () => {
  const projects = []

  return (
    <DashboardLayout>
      <div className="projects-page">
        {projects.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📁</div>
            <h2>No projects yet</h2>
            <p>Create your first project to get started with budget controls and spending rules</p>
            <button className="btn btn-primary">Create Project</button>
          </div>
        ) : (
          <>
            <div className="projects-grid">
              {projects.map((project) => (
                <div key={project.id} className="project-card">
                  <div className="project-header">
                    <h3>{project.name}</h3>
                    <span className="project-status">{project.status}</span>
                  </div>
                  <p className="project-description">{project.description}</p>
                  <div className="project-stats">
                    <div className="project-stat">
                      <span className="stat-label">Budget</span>
                      <span className="stat-value">{project.budget}</span>
                    </div>
                    <div className="project-stat">
                      <span className="stat-label">Spent</span>
                      <span className="stat-value">{project.spent}</span>
                    </div>
                    <div className="project-stat">
                      <span className="stat-label">Requests</span>
                      <span className="stat-value">{project.requests}</span>
                    </div>
                  </div>
                  <div className="project-actions">
                    <button className="btn btn-outline">View Details</button>
                    <button className="btn btn-primary">Manage</button>
                  </div>
                </div>
              ))}
            </div>
            <div className="page-actions-bottom">
              <button className="btn btn-primary">Create Project</button>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  )
}

export default Projects

