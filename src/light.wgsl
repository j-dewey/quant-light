// this just takes a quad representing the screen
struct VertInput{
    @location(0) position: vec2<f32>
}

@vertex
fn vs_main(in: VertInput) -> FragInput {
    var out: FragInput;
    out.uv = vec4<f32>(
        in.position[0],
        in.position[1],
        1.0,
        1.0
    );
    out.screen_space = vec2(
        (in.position[0] + 1.0) / 2.0,
        (-in.position[1] + 1.0) / 2.0
    );
    return out;
}

//
// Fragment
//

struct FragInput{
    @builtin(position) uv: vec4<f32>,
    @location(0) screen_space: vec2<f32>
}

// quantized colors
@group(0) @binding(0)
var color_text: texture_2d<f32>;
@group(0) @binding(1)
var color_samp: sampler;

struct LightDetails{
    @location(0) x: f32,
    @location(1) y: f32,
    // light will decrease linearly from (position) to (position + max_out_at)
    @location(2) max_out_at: f32
}

@group(1) @binding(0)
var<uniform> light: LightDetails;

@fragment
fn fs_main(in: FragInput) -> @location(0) vec4<f32> {
    let dist_from_light_x = in.screen_space[0] - light.x;
    let dist_from_light_y = in.screen_space[1] - light.y;
    let dist = sqrt(dist_from_light_x*dist_from_light_x + dist_from_light_y*dist_from_light_y);
    let mult = dist/light.max_out_at;

    let samp = textureSample(color_text, color_samp, vec2(mult, 0.0));
    return samp;
}
