#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <boost/date_time.hpp>

namespace bt = boost::posix_time;

class User {
public:
    std::string name;
    std::string email;
    std::vector<std::string> skills;

    User(std::string n, std::string e) : name(n), email(e) {}
};

class Skill {
public:
    std::string title;
    std::string description;
    std::string category;
    int ratingSum;
    int numRatings;

    Skill(std::string t, std::string d, std::string c) : title(t), description(d), category(c), ratingSum(0), numRatings(0) {}
};

class SkillSession {
public:
    int sessionID;
    User provider;
    User requester;
    Skill skill;
    bt::ptime startTime;

    SkillSession(int id, User p, User r, Skill s, bt::ptime st) : sessionID(id), provider(p), requester(r), skill(s), startTime(st) {}
};

class CommunitySkillSharingPlatform {
private:
    std::vector<User> users;
    std::vector<Skill> skills;
    std::vector<SkillSession> sessions;

public:
    void addUser(User user) {
        users.push_back(user);
    }

    void addSkill(User& user, Skill skill) {
        user.skills.push_back(skill.title);
        skills.push_back(skill);
    }

    void requestSkillSession(User& requester, User& provider, Skill& skill) {
        bt::ptime now = bt::second_clock::local_time();
        bt::ptime startTime = now + bt::hours(24);
        SkillSession session(sessions.size() + 1, provider, requester, skill, startTime);
        sessions.push_back(session);

        std::cout << requester.name << " requested a skill session with " << provider.name << " for skill: " << skill.title << std::endl;
        std::cout << "Session scheduled at: " << bt::to_simple_string(startTime) << std::endl;
    }

    void displayUserSkills(User& user) {
        std::cout << user.name << "'s Skills:" << std::endl;
        for (const std::string& skillTitle : user.skills) {
            std::cout << "Skill: " << skillTitle << std::endl;
        }
    }

    void displaySessions(User& user) {
        std::cout << "Sessions for " << user.name << ":" << std::endl;
        for (const SkillSession& session : sessions) {
            if (session.requester.name == user.name || session.provider.name == user.name) {
                std::cout << "Session ID: " << session.sessionID << std::endl;
                std::cout << "Provider: " << session.provider.name << std::endl;
                std::cout << "Requester: " << session.requester.name << std::endl;
                std::cout << "Skill: " << session.skill.title << std::endl;
                std::cout << "Start Time: " << bt::to_simple_string(session.startTime);
                std::cout << std::endl;
            }
        }
    }
};

int main() {
    CommunitySkillSharingPlatform platform;

    User user1{"Alice", "alice@example.com"};
    User user2{"Bob", "bob@example.com"};
    platform.addUser(user1);
    platform.addUser(user2);

    Skill skill1{"Cooking Basics", "Learn the fundamentals of cooking.", "Cooking"};
    Skill skill2{"Introduction to Programming", "Get started with coding.", "Coding"};

    platform.addSkill(user1, skill1);
    platform.addSkill(user2, skill2);

    bt::ptime startTime;
    bt::ptime now = bt::second_clock::local_time();
    startTime = now + bt::hours(24);

    platform.requestSkillSession(user1, user2, skill2);

    platform.displayUserSkills(user1);
    platform.displayUserSkills(user2);
    platform.displaySessions(user1);

    return 0;
}
