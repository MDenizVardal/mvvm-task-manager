package com.example.amadlab

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import kotlinx.serialization.Serializable

@Serializable
object TaskList

@Serializable
data class TaskDetail(val taskId: Long)

// Task 3.4: third destination, without arguments
@Serializable
object Statistics

// Task 3.4: set to false to see what happens without launchSingleTop
const val STATISTICS_SINGLE_TOP = true

@Composable
fun AmadLabNavHost(navController: NavHostController = rememberNavController()) {
    // logs the entry on top of the back stack every time it changes (used in task 3.4)
    LaunchedEffect(navController) {
        navController.currentBackStackEntryFlow.collect { entry ->
            val name = entry.destination.route?.substringAfterLast('.')
            Log.d("BackStack", "top = $name, entry ${entry.id.take(8)}")
        }
    }

    NavHost(navController = navController, startDestination = TaskList) {
        composable<TaskList> {
            TaskListRoute(
                onTaskClick = { id -> navController.navigate(TaskDetail(id)) },
                onStatisticsClick = {
                    navController.navigate(Statistics) {
                        launchSingleTop = STATISTICS_SINGLE_TOP
                    }
                }
            )
        }
        composable<TaskDetail> {
            TaskDetailRoute(onBack = { navController.popBackStack() })
        }
        composable<Statistics> {
            StatisticsRoute(onBack = { navController.popBackStack() })
        }
    }
}
