package com.example.amadlab.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Same colours as in my lab 02 project (task 2.1.5)
private val Teal40 = Color(0xFF00696B)
private val Teal80 = Color(0xFF80D4D5)
private val Teal90 = Color(0xFF9CF1F2)
private val Teal30 = Color(0xFF004F51)
private val Orange40 = Color(0xFF9A4521)
private val Orange80 = Color(0xFFFFB597)

private val LightColors = lightColorScheme(
    primary = Teal40,
    primaryContainer = Teal90,
    secondary = Orange40
)

private val DarkColors = darkColorScheme(
    primary = Teal80,
    primaryContainer = Teal30,
    secondary = Orange80
)

@Composable
fun AmadLabTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        typography = Typography(),
        content = content
    )
}
