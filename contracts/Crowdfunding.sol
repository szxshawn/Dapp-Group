// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Crowdfunding {
    struct Project {
        address owner;
        string name;
        string description;
        uint goal;
        uint pledged;
        bool completed;
        string userAccount; 
    }

    Project[] public projects;

    function createProject(string memory _name, string memory _description, uint _goal, string memory _userAccount) public {
        projects.push(Project({
            owner: msg.sender,
            name: _name,
            description: _description,
            goal: _goal,
            pledged: 0,
            completed: false,
            userAccount: _userAccount 
        }));
    }

    function pledge(uint _projectId) public payable {
        Project storage project = projects[_projectId];
        require(!project.completed, "Project already completed");
        project.pledged += msg.value;
        if (project.pledged >= project.goal) {
            project.completed = true;
        }
    }

    function getProject(uint _projectId) public view returns (address, string memory, string memory, uint, uint, bool, string memory) {
        Project storage project = projects[_projectId];
        return (project.owner, project.name, project.description, project.goal, project.pledged, project.completed, project.userAccount);
    }

    function getProjectsCount() public view returns (uint) {
        return projects.length;
    }
}
