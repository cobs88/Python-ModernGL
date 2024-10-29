#version 460 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;  // Ambient intensity
    vec3 Id;  // Diffuse intensity
    vec3 Is;  // Specular intensity
};

uniform Light lights[10];  // Change size as needed
uniform int lightCount;    // Number of active lights
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal); // Get normal

    // Ambient lighting
    vec3 ambient = vec3(0.0);
    int numLights = 0; // Count how many lights we will consider

    // Loop through each light
    for (int i = 0; i < 10; ++i) { // Assuming you have a maximum of 10 lights
        if (i < lightCount) { // Only consider active lights
            ambient += lights[i].Ia; // Accumulate ambient contribution
            numLights++; // Increment count of active lights
        }
    }

    // Scale the ambient lighting based on the number of lights
    ambient *= (1.0 / float(numLights)); // Average ambient

    // Diffuse lighting
    vec3 diffuse = vec3(0.0);
    for (int i = 0; i < numLights; ++i) {
        vec3 lightDir = normalize(lights[i].position - fragPos);
        float diff = max(0, dot(lightDir, Normal));
        diffuse += diff * lights[i].Id; // Accumulate diffuse contributions
    }

    // Specular lighting
    vec3 specular = vec3(0.0);
    for (int i = 0; i < numLights; ++i) {
        vec3 lightDir = normalize(lights[i].position - fragPos);
        vec3 viewDir = normalize(camPos - fragPos);
        vec3 reflectDir = reflect(-lightDir, Normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
        specular += spec * lights[i].Is; // Accumulate specular contributions
    }

    // Combine color with lighting
    return color * (ambient + diffuse + specular);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;

    color = pow(color, vec3(gamma)); // Apply gamma correction

    color = getLight(color); // Calculate lighting

    color = pow(color, vec3(1.0 / gamma)); // Reverse gamma correction
    fragColor = vec4(color, 1.0);
}
